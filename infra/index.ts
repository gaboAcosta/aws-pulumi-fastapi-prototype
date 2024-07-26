import * as aws from "@pulumi/aws";
import * as awsx from "@pulumi/awsx";
import * as pulumi from "@pulumi/pulumi";

const config = new pulumi.Config();
export const imageTag = config.require("image_tag");
export const appName = config.require("app_name");

// An ECS cluster to deploy into.
const cluster = new aws.ecs.Cluster(`${appName}-cluster`, {});

// Create a load balancer to listen for requests and route them to the container.
const loadBalancer = new awsx.lb.ApplicationLoadBalancer(`${appName}-lb`, {});

const dbCreds = new aws.secretsmanager.Secret('app-credentials', {
    description: "RDS database postgres credentials for the app",
    name: `${appName}-credentials`,
}, {
    protect: true,
});

const baseContainerSettings = {
    name: "awsx-ecs",
    image: `471112624128.dkr.ecr.us-east-2.amazonaws.com/${appName}:${imageTag}`,
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
            valueFrom: pulumi.interpolate`${dbCreds.arn}:host::`,
        },
        {
            name: "DATABASE_PORT",
            valueFrom: pulumi.interpolate`${dbCreds.arn}:port::`,
        },
        {
            name: "DATABASE_USER",
            valueFrom: pulumi.interpolate`${dbCreds.arn}:username::`,
        },
        {
            name: "DATABASE_PASSWORD",
            valueFrom: pulumi.interpolate`${dbCreds.arn}:password::`,
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
const service = new awsx.ecs.FargateService(`${appName}-service`, {
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



const migrationsTask = new awsx.ecs.FargateTaskDefinition(`${appName}-migrations-td`, {
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
export const frontendURL = pulumi.interpolate `http://${loadBalancer.loadBalancer.dnsName}/docs`;