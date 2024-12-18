"""A Python Pulumi program"""

import pulumi
import pulumi_docker_build as docker_build
import pulumi_aws as aws

# labels = docker_build.Image("labels",
#     push=False,
#     load=True,
#     context=docker_build.BuildContextArgs(
#         location="./app",
#     ),
#     labels={
#         "description": "This image will get a descriptive label 👍",
#     })

base_name="refresh"

ecr_repository = aws.ecr.Repository(
    f"{base_name}-ecr-repository",
    force_delete=True,
)

auth_token = aws.ecr.get_authorization_token_output(registry_id=ecr_repository.registry_id)

ecr_image = docker_build.Image(
            f"{base_name}_db_export_lambda_image",
            context={
                "location": "./app",
            },
            push=True,
            platforms=[
                docker_build.Platform.LINUX_ARM64,
            ],
            tags=[ecr_repository.repository_url.apply(lambda repository_url: f"{repository_url}:latest")],
            build_on_preview=True,
            registries=[
                docker_build.RegistryArgs(
                    address=ecr_repository.repository_url,
                    username=auth_token.user_name,
                    password=auth_token.password,
                )
            ],
            # opts=pulumi.ResourceOptions(ignore_changes=["context"]),
        )