# Snoopy

### What is snoopy!

The "Snoopy" boilerplate in flask framework for development enterprise application.

### Motivation

In my 10 years of development experience, I have worked on many b2b projects. In many projects I have come across typically for b2b problems, example
   1. The inability to maintenance from growing source code base.
   2. Sensitive to change. 
   3. There is no certainty that your code is working or is working correctly. 
   4. To transfer some part to microservice, you need to rewrite the whole project.

and others, this project should solve many of these problems

### Snoopy vs Other framework

| Feature                                                                  | Snoopy | Django         | Flask Core |
|--------------------------------------------------------------------------|--------|----------------|------------|
| Service Layer for separate business logics                               | ✓      | -              | -          |
| Code generate from OpenAPI schemas (Swagger)                             | ✓      | -              | -          |
| Fixtures for pre-populate your database with hard-coded data for testing | ✓      | ✓              | -          |
| API friendly                                                             | ✓      | ✓RestFramework | -          |
| SqlAlchemy                                                               | ✓      | -              | ✓          |
| Django based settings                                                    | ✓      | ✓              | -          |


### Roadmap

0.2.0 Forgot password feature in auth module

0.3.0 DDD architecture

0.4.0 from boilerplate to framework

0.5.0 Auto generate template for new project

0.6.0 Support graphql

### Get started!

```
$ chmod +x bin/*

$ ./bin/install
$ ./bin/start
```

