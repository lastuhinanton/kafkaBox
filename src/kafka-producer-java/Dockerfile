# 1) Сборка
FROM maven:3.6-jdk-8 AS build
WORKDIR /app
COPY pom.xml .
COPY src ./src
RUN mvn clean package -DskipTests

# 2) Runtime
FROM openjdk:8-jre
WORKDIR /app
COPY --from=build /app/target/kafka-producer-1.0-SNAPSHOT.jar ./app.jar
COPY src/main/resources/log4j.properties ./log4j.properties

ENTRYPOINT ["java", "-Dlog4j.configurationFile=log4j.properties", "-jar", "app.jar"]