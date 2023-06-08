from aws_cdk import (
    aws_codecommit as codecommit,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    aws_codebuild as codebuild,
    aws_codedeploy as codedeploy,
    aws_ecs as ecs,
    aws_events as events,
    aws_events_targets as targets,
    Stack,
)
from constructs import Construct
from app.base_stack import BaseStack


class PipelineDeployStack(BaseStack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        repo = codecommit.Repository.from_repository_name(
            self, "ark-ledger", "ark-ledger-pipeline-test"
        )

        build_project = codebuild.PipelineProject(
            self,
            "ark-build-project",
            build_spec=codebuild.BuildSpec.from_object(
                {
                    "version": "0.2",
                    "phases": {
                        "install": {
                            "runtime-versions": {"python": "3.8"},
                            "commands": [
                                "pip install awscli",
                                "ls -lah",
                            ],
                        },
                        "build": {
                            "commands": ['echo "Building the application"', "ls -lah"]
                        },
                        "post_build": {
                            "commands": ['echo "Running unit tests"', "ls -lah"]
                        },
                    },
                }
            ),
            environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxBuildImage.AMAZON_LINUX_2_3,
            ),
        )

        pipeline = codepipeline.Pipeline(
            self,
            "ark-code-pipeline-deploy",
            pipeline_name=self.STACK_PREFIX + "ark-code-pipeline-deploy",
            cross_account_keys=False,
            restart_execution_on_update=True,
        )

        source = codepipeline.Artifact("SourceOutput")

        source_action = codepipeline_actions.CodeCommitSourceAction(
            action_name="Source",
            output=source,
            repository=repo,
            branch="main",
            trigger=codepipeline_actions.CodeCommitTrigger.POLL,
        )

        pipeline.add_stage(stage_name="Source", actions=[source_action])

        build_action = codepipeline_actions.CodeBuildAction(
            action_name="Build",
            project=build_project,
            input=source,
            outputs=[codepipeline.Artifact("BuildOutput")],
        )
        pipeline.add_stage(stage_name="Build", actions=[build_action])

        events.Rule(
            self,
            "ark-gl-pipeline-deploy-rule",
            description="Trigger notifications based on CodeCommit PullRequests for Deployment",
            event_pattern=events.EventPattern(
                source=["aws.codecommit"],
                detail_type=["CodeCommit Pull Request State Change"],
                resources=[repo.repository_arn],
                detail={
                    "event": ["pullRequestMergeStatusUpdated"],
                    "isMerged": ["True"],
                },
            ),
            targets=[
                targets.CodePipeline(
                    pipeline,
                )
            ],
        )
