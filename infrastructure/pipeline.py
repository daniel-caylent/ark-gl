from aws_cdk import (
    aws_codecommit as codecommit,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    aws_codebuild as codebuild,
    aws_codedeploy as codedeploy,
    aws_ecs as ecs,
    Stack
)
from constructs import Construct
from app.base_stack import BaseStack



class PipelineStack(BaseStack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Define the CodeCommit repository
        repo = codecommit.Repository.from_repository_name(self, 'ark-ledger', 'ark-ledger')

        # Define the CodeBuild project
        build_project = codebuild.PipelineProject(self, 'ark-build-project',
            build_spec=codebuild.BuildSpec.from_object({
                'version': '0.2',
                'phases': {
                    'install': {
                        'runtime-versions': {
                            'python': '3.8'
                        },
                        'commands': [
                            'pip install awscli',
                            'ls -lah',
                        ]
                    },
                    'build': {
                        'commands': [
                            'echo "Building the application"',
                            'ls -lah'
                        ]
                    },
                    'post_build': {
                        'commands': [
                            'echo "Running unit tests"',
                            'ls -lah'
                        ]
                    }
                }
            }),
            environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxBuildImage.AMAZON_LINUX_2_3,
            )
        )

        # Define the CodeDeploy ECS application
        #ecs_application = ecs.EcsApplication(self, 'MyEcsApplication',
        #    application_name='my-ecs-app'
        #)

        # Define the pipeline
        pipeline = codepipeline.Pipeline(self, 'ark-code-pipeline',
            pipeline_name='ark-code-pipeline',
            cross_account_keys=False,
            restart_execution_on_update=True
        )

        source = codepipeline.Artifact('SourceOutput')

        # Add the CodeCommit source action to the pipeline
        source_action = codepipeline_actions.CodeCommitSourceAction(
            action_name='Source',
            output=source,
            repository=repo,
            branch='main',
            trigger=codepipeline_actions.CodeCommitTrigger.POLL
        )
        pipeline.add_stage(
            stage_name='Source',
            actions=[source_action]
        )

        # Add the CodeBuild build action to the pipeline
        build_action = codepipeline_actions.CodeBuildAction(
            action_name='Build',
            project=build_project,
            input=source,
            outputs=[codepipeline.Artifact('BuildOutput')]
        )
        pipeline.add_stage(
            stage_name='Build',
            actions=[build_action]
        )

        # Add the CodeDeploy deploy action to the pipeline
        #deploy_action = codepipeline_actions.EcsDeployAction(
        #    action_name='Deploy',
        #    service=ecs_application.default_service,
        #    image_file=codepipeline.ArtifactPath(
        #        build_action.output,
        #        'imagedefinitions.json'
        #    ),
        #    deployment_timeout=core.Duration.minutes(30),
        #    app_spec_template_file=codepipeline.ArtifactPath(
        #        build_action.output,
        #        'appspec.yml'
        #    )
        #)
        #pipeline.add_stage(
        #    stage_name='Deploy',
        #    actions=[deploy_action]
        #)
