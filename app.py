import aws_cdk as cdk

# importa tu stack; asegúrate de que el paquete y el nombre coincidan
from cdk_ec2_lab.cdk_ec2_lab_stack import CdkEc2LabStack

# 1. crea la aplicación CDK
app = cdk.App()

# 2. instancia tu stack dentro de la app
CdkEc2LabStack(
    app,
    "CdkEc2LabStack",
    env=cdk.Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"),
        region=os.getenv("CDK_DEFAULT_REGION"),
    ),
)

# 3. sintetiza la plantilla
app.synth()