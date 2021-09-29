# YOURWAY WARNING JOB
<img width="800" alt="warning yourway" src="https://user-images.githubusercontent.com/50447619/130323874-63729001-4f17-4c72-afb5-22542de9c861.png">

Warning Job Yourway is a job alert system for users on [Yourway](https://yourway.vn)

## Prerequisites & Documentation

Make sure to install enough requirements before continue. All requirements are listed below:

* Operating systems: Linux, macOS
* Java version >= 11
* [Spark 3.x](https://spark.apache.org/downloads.html) & [docs](https://spark.apache.org/docs/latest/)
* [Kafka 2.x](https://kafka.apache.org/quickstart) & [docs](https://kafka.apache.org/documentation/)
* Maven

Config kafka information in class Settings then run the following command to build file jar:

    mvn install

## Usage
### Start job user query

    spark-submit out/artifacts/userquery/yourway_warning_job.jar

### Start job warning job

    spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 out/artifacts/userquery/yourway_warning_job.jar

# Yourway_job_alert - backend

This application was generated using JHipster 7.2.0, you can find documentation and help at [https://www.jhipster.tech/documentation-archive/v7.2.0](https://www.jhipster.tech/documentation-archive/v7.2.0).

## Development

To start your application in the dev profile, run:

```
./mvnw
```

For further instructions on how to develop with JHipster, have a look at [Using JHipster in development][].

### JHipster Control Center

JHipster Control Center can help you manage and control your application(s). You can start a local control center server (accessible on http://localhost:7419) with:

```
docker-compose -f src/main/docker/jhipster-control-center.yml up
```

### Doing API-First development using openapi-generator

[OpenAPI-Generator]() is configured for this application. You can generate API code from the `src/main/resources/swagger/api.yml` definition file by running:

```bash
./mvnw generate-sources
```

Then implements the generated delegate classes with `@Service` classes.

To edit the `api.yml` definition file, you can use a tool such as [Swagger-Editor](). Start a local instance of the swagger-editor using docker by running: `docker-compose -f src/main/docker/swagger-editor.yml up -d`. The editor will then be reachable at [http://localhost:7742](http://localhost:7742).

Refer to [Doing API-First development][] for more details.

## Building for production

### Packaging as jar

To build the final jar and optimize the Yourway_job_alert application for production, run:

```
./mvnw -Pprod clean verify
```

To ensure everything worked, run:

```
java -jar target/*.jar
```

Refer to [Using JHipster in production][] for more details.

### Packaging as war

To package your application as a war in order to deploy it to an application server, run:

```
./mvnw -Pprod,war clean verify
```

## Testing

To launch your application's tests, run:

```
./mvnw verify
```

### Other tests

Performance tests are run by [Gatling][] and written in Scala. They're located in [src/test/gatling](src/test/gatling).

To use those tests, you must install Gatling from [https://gatling.io/](https://gatling.io/).

For more information, refer to the [Running tests page][].

### Code quality

Sonar is used to analyse code quality. You can start a local Sonar server (accessible on http://localhost:9001) with:

```
docker-compose -f src/main/docker/sonar.yml up -d
```

Note: we have turned off authentication in [src/main/docker/sonar.yml](src/main/docker/sonar.yml) for out of the box experience while trying out SonarQube, for real use cases turn it back on.

You can run a Sonar analysis with using the [sonar-scanner](https://docs.sonarqube.org/display/SCAN/Analyzing+with+SonarQube+Scanner) or by using the maven plugin.

Then, run a Sonar analysis:

```
./mvnw -Pprod clean verify sonar:sonar
```

If you need to re-run the Sonar phase, please be sure to specify at least the `initialize` phase since Sonar properties are loaded from the sonar-project.properties file.

```
./mvnw initialize sonar:sonar
```

For more information, refer to the [Code quality page][].

## Using Docker to simplify development (optional)

You can use Docker to improve your JHipster development experience. A number of docker-compose configuration are available in the [src/main/docker](src/main/docker) folder to launch required third party services.

For example, to start a mysql database in a docker container, run:

```
docker-compose -f src/main/docker/mysql.yml up -d
```

To stop it and remove the container, run:

```
docker-compose -f src/main/docker/mysql.yml down
```

You can also fully dockerize your application and all the services that it depends on.
To achieve this, first build a docker image of your app by running:

```
./mvnw -Pprod verify jib:dockerBuild
```

Then run:

```
docker-compose -f src/main/docker/app.yml up -d
```

For more information refer to [Using Docker and Docker-Compose][], this page also contains information on the docker-compose sub-generator (`jhipster docker-compose`), which is able to generate docker configurations for one or several JHipster applications.

## Continuous Integration (optional)

To configure CI for your project, run the ci-cd sub-generator (`jhipster ci-cd`), this will let you generate configuration files for a number of Continuous Integration systems. Consult the [Setting up Continuous Integration][] page for more information.

[jhipster homepage and latest documentation]: https://www.jhipster.tech
[jhipster 7.2.0 archive]: https://www.jhipster.tech/documentation-archive/v7.2.0
[using jhipster in development]: https://www.jhipster.tech/documentation-archive/v7.2.0/development/
[using docker and docker-compose]: https://www.jhipster.tech/documentation-archive/v7.2.0/docker-compose
[using jhipster in production]: https://www.jhipster.tech/documentation-archive/v7.2.0/production/
[running tests page]: https://www.jhipster.tech/documentation-archive/v7.2.0/running-tests/
[code quality page]: https://www.jhipster.tech/documentation-archive/v7.2.0/code-quality/
[setting up continuous integration]: https://www.jhipster.tech/documentation-archive/v7.2.0/setting-up-ci/
[node.js]: https://nodejs.org/
[npm]: https://www.npmjs.com/
[gatling]: https://gatling.io/
[openapi-generator]: https://openapi-generator.tech
[swagger-editor]: https://editor.swagger.io
[doing api-first development]: https://www.jhipster.tech/documentation-archive/v7.2.0/doing-api-first-development/
