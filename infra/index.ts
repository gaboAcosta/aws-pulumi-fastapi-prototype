import * as aws from "@pulumi/aws";
import * as awsx from "@pulumi/awsx";
import * as pulumi from "@pulumi/pulumi";

const config = new pulumi.Config();
export const imageTag = config.require("image_tag");

// An ECS cluster to deploy into.
const cluster = new aws.ecs.Cluster("pulumi-flask-cluster", {});

// Create a load balancer to listen for requests and route them to the container.
const loadBalancer = new awsx.lb.ApplicationLoadBalancer("pulumi-flask-lb", {});

const dbcreds = new aws.secretsmanager.Secret("dbcreds", {
    description: "RDS database postgres credentials for database-1",
    name: "rds-db-credentials/cluster-IODSIQ5QKFEEIUDQVGGHGBQUCE/postgres/1721919538454",
}, {
    protect: true,
});

const baseContainerSettings = {
    name: "awsx-ecs",
    image: `471112624128.dkr.ecr.us-east-2.amazonaws.com/fastapi-prototype:${imageTag}`,
    cpu: 128,
    memory: 512,
    essential: true,
    portMappings: [{
        containerPort: 80,
        targetGroup: loadBalancer.defaultTargetGroup,
    }],
    environment: [
        {
            name: "ENV",
            value: "development",
        },
        {
            name: "DATABASE_NAME",
            value: 'postgres',
        },
    ],
    secrets: [
        {
            name: "DATABASE_HOST",
            valueFrom: pulumi.interpolate`${dbcreds.arn}:host::`,
        },
        {
            name: "DATABASE_PORT",
            valueFrom: pulumi.interpolate`${dbcreds.arn}:port::`,
        },
        {
            name: "DATABASE_USER",
            valueFrom: pulumi.interpolate`${dbcreds.arn}:username::`,
        },
        {
            name: "DATABASE_PASSWORD",
            valueFrom: pulumi.interpolate`${dbcreds.arn}:password::`,
        },
    ],
};

const executionRolePolicies = [
    {
        name: "allow-asm",
        policy: '{"Statement": [{"Action": "secretsmanager:GetSecretValue", "Effect": "Allow", "Resource": "*"}]}',
    }
]

// Define the service and configure it to use our image and load balancer.
const service = new awsx.ecs.FargateService("pulumi-flask-service", {
    cluster: cluster.arn,
    assignPublicIp: true,
    taskDefinitionArgs: {
        container: baseContainerSettings,
        executionRole: {
            args: {
                inlinePolicies: executionRolePolicies
            }
        }
    },
});



const migrationsTask = new awsx.ecs.FargateTaskDefinition("pulumi-flask-service-migrations-td", {
    container: {
        ...baseContainerSettings,
        entryPoint: ["/usr/bin/make"],
        command: ["migrate"],
    },
    executionRole: {
        args: {
            inlinePolicies: executionRolePolicies
        }
    }
})



// Export the URL so we can easily access it.
export const frontendURL = pulumi.interpolate `http://${loadBalancer.loadBalancer.dnsName}`;