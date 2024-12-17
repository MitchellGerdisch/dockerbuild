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

base_name="mitch"

ecr_repository = aws.ecr.Repository(
    f"{base_name}-ecr-repository",
    # image_scanning_configuration=aws.ecr.RepositoryImageScanningConfigurationArgs(
    #     scan_on_push=True
    # ),
    # image_tag_mutability="MUTABLE",
    # tags={
    #     "Environment": "dev",
    # }
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
            # opts=pulumi.ResourceOptions(
            #   ignore_changes=["contextHash"]
            # )
            #     aliases=[pulumi.Alias(parent=pulumi.ROOT_STACK_RESOURCE)], parent=self, ignore_changes=["contextHash"]
            # ),
        )