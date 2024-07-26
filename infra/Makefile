# Install Pulumi CLI
install-pulumi:
	curl -fsSL https://get.pulumi.com | sh

config-pulumi:
	pulumi config set aws:region us-east-1

# Login to Pulumi
login-pulumi:
	pulumi login s3://endless-health-infrastructure/pullumi-flask-ecs-prototype

# Create a new stack
create-stack:
	pulumi stack init <stack-name>

# Select a stack
select-stack:
	pulumi stack select <stack-name>

# Preview changes
preview:
	pulumi preview

# Deploy changes
deploy:
	pulumi up

# Destroy stack
destroy:
	pulumi destroy

# Show current stack information
stack-info:
	pulumi stack

# Show current stack outputs
stack-outputs:
	pulumi stack output