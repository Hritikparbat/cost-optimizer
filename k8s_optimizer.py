from kubernetes import client, config

# Load kube config (Minikube)
config.load_incluster_config()

v1 = client.CoreV1Api()
apps_v1 = client.AppsV1Api()

THRESHOLD_CPU = 10  # in millicores (very low)

def get_pod_metrics():
    from subprocess import check_output
    output = check_output("kubectl top pods --no-headers", shell=True).decode()
    return output

def scale_deployment(deployment_name, namespace, replicas):
    body = {'spec': {'replicas': replicas}}
    apps_v1.patch_namespaced_deployment_scale(
        name=deployment_name,
        namespace=namespace,
        body=body
    )
    print(f"Scaled {deployment_name} to {replicas} replicas")

def main():
    pods = v1.list_namespaced_pod(namespace="default")

    metrics = get_pod_metrics()

    for pod in pods.items:
        name = pod.metadata.name
        print(f"Checking pod: {name}")

        if name in metrics:
            cpu_usage = int(metrics.split(name)[1].split()[0].replace('m', ''))

            print(f"CPU: {cpu_usage}m")

            if cpu_usage < THRESHOLD_CPU:
                print("Low usage → scaling down")

                # Assume deployment name = nginx
                scale_deployment("nginx", "default", 1)
                break
            else:
                print("Pod is active")

if __name__ == "__main__":
    main()