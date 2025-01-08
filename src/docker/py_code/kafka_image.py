import sys, os, docker
from parse_kafka_versions import receive_version

def build_dockerfile(app_name, version):
  client = docker.from_env()
  try:
    image, logs = client.images.build(
      path=".",
      tag=f"{app_name}:{version}",
      dockerfile=f"{app_name}_{version}.dockerfile"
    )
    for log in logs:
      if "stream" in log: print(log["stream"].strip())
  except docker.errors.BuildError as e:
    print(f"Build error: {str(e)}")
  except docker.errors.APIError as e:
    print(f"Docker API error: {str(e)}")
  finally:
    os.remove(f"{app_name}_{version}.dockerfile")

def push_image(app_name, version, rep_name):
  tag_name = f"{rep_name}/{app_name}:{version}" 
  client = docker.from_env()
  try:
    image = client.images.get(f"{app_name}:{version}") 
    image.tag(tag_name)
    push_logs = client.images.push(tag_name, stream=True, decode=True)
    for log in push_logs:
      if "status" in log: print(log["status"])
      if "error" in log: print(f"Error: {log['error']}")
  except docker.errors.ImageNotFound:
    print(f"Error: Image {app_name}:{version} not found.")
  except docker.errors.APIError as e:
    print(f"Docker API error: {str(e)}")

def push_broker_image(version, rep_name):
  app_name = "kafka_broker"
  image_name = f"{app_name}_{version}"
  with open(f"{image_name}.dockerfile", "w") as f:
    f.write(f"FROM apache/kafka:{version}\n")
    f.write("WORKDIR /opt/kafka\n")
    f.write("USER root\n")
    f.write("COPY kafkaBrokerEntrypoint.sh /entrypoint.sh\n")
    f.write("RUN chmod +x /entrypoint.sh\n")
    f.write('CMD ["/bin/sh", "-c", "/entrypoint.sh && /opt/kafka/bin/kafka-server-start.sh /opt/kafka/config/server.properties"]\n')
  build_dockerfile(app_name, version)
  push_image(app_name, version, rep_name)

def push_zookeeper_image(version, rep_name):
  app_name = "zookeeper"
  image_name = f"{app_name}_{version}"
  with open(f"{image_name}.dockerfile", "w") as f:
    f.write(f"FROM apache/kafka:{version}\n")
    f.write("WORKDIR /opt/kafka\n")
    f.write("USER root\n")
    f.write("COPY zkEntrypoint.sh /entrypoint.sh\n")
    f.write("RUN chmod +x /entrypoint.sh\n")
    f.write('CMD ["/bin/sh", "-c", "/entrypoint.sh && /opt/kafka/bin/zookeeper-server-start.sh /opt/kafka/config/zookeeper.properties"]\n')
  build_dockerfile(app_name, version)
  #push_image(app_name, version, rep_name)

def create_image():
  answer = "yYyesYESYesyeYEYeyeahYEAHYeah"
  rep_name = "antonlastukhin"
  version = receive_version()
  if input("\nCreate broker image?") in answer: push_broker_image(version, rep_name)
  if input("\nCreate zookeeper image?") in answer: push_zookeeper_image(version, rep_name)

if __name__ == "__main__":
  create_image()

