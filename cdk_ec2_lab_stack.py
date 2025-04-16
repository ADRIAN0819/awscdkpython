from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
    CfnOutput,
)
from constructs import Construct

class CdkEc2LabStack(Stack):
    """Creates one Ubuntu 22.04 EC2 instance ready for SSH (22) & HTTP (80)."""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 1. Default VPC
        vpc = ec2.Vpc.from_lookup(self, "DefaultVpc", is_default=True)

        # 2. Seguridad Grupo con los puertos 22 (SSH) y 80 (HTTP)
        sg = ec2.SecurityGroup(
            self, "WebSg",
            vpc=vpc,
            description="Allow SSH & HTTP",
                        allow_all_outbound=True
        )
        sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "Allow SSH")
        sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "Allow HTTP")

        # 3. Usar la 22.04 AMI ID encontrada en AWS Academy Cloud9ubuntu22
        ami = ec2.GenericLinuxImage({
            "us-east-1": "ami-0363234289a7b6202"
        })

        # 4. IAM Role de AWS Academy
        lab_role = iam.Role.from_role_arn(
            self, "LabRole",
            role_arn="arn:aws:iam::254780740814:role/LabRole",
            mutable=False
        )

        # 5. EC2 Instancia 
        instance = ec2.Instance(
            self, "WebServer",
              instance_type=ec2.InstanceType("t3.micro"),
            machine_image=ami,
            vpc=vpc,
            security_group=sg,
            key_name="vockey",
            role=lab_role,
            block_devices=[
                ec2.BlockDevice(
                    device_name="/dev/xvda",
                    volume=ec2.BlockDeviceVolume.ebs(
                        volume_size=20,
                        volume_type=ec2.EbsDeviceVolumeType.GP3,
                        delete_on_termination=True
                    )
                )
                        ],
        )

        # 6. Output 
        CfnOutput(self, "PublicDNS", value=instance.instance_public_dns_name)
        CfnOutput(self, "InstanceId", value=instance.instance_id)