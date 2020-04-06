# D5 Design

## Description
Httpfs addresses the problem of the lack of a simple, fast, and secure network filesystem. This problem plagues developers and IT administrators who need a filesystem over a network. The current solution, NFS, was originally developed in the 1980s. It is overused and has no viable alternative. Httpfs solves this problem. It is an easy-to-setup remote storage solution that is built for developers and IT administrators. Httpfs is a network filesystem that is easy-to-use, like NFS, but, unlike NFS, is also fast, secure. It is also cross-platform, and makes it easy to access your data in the cloud from any operating system.

[Github Repo](https://github.com/httpfs/httpfs)

[Trello Board](https://trello.com/b/cY9hPQYZ/httpfs)


## Architecture
![](https://i.imgur.com/eGTaxEE.png)

Our application has a client-server structure, so we naturally seperated our app at the top package level into client and server packages. There are some attributes and methods that both the client and the server share; we placed those in a common package. Both client and server each have a driver package called \_\_main__. This is the package that contains the logic to setup and run each side of the application.


## Class Diagram
![](https://i.imgur.com/5XRL6oW.png)



## Sequence Diagram

### Client Write Use Case Sequence Diagram

![](https://i.imgur.com/bgI030m.png)

### Client Wrie Use Case Description

1. **Brief Description:** write to a file on server
2. **Actor Description:** Client side file editor
3. **Pre-conditions**:
    - Httpfs is installed
    - User is authorized to access server
4. **Basic Flow**:
    1. User issues write command to he HttpFsClient
    2. The HttpFsClient sends a request to HttpsFsRequestHandler
    3. HttpsFsRequestHandler unpacks response, validates it. and then sends write command to HttpFs Server
    4. HttpsFs Server sends result back to HttpFs Client
5. **Alternative Flows**:
    3.a The User doest not have write permission to directory or file requested and the HttpFsRequestHandler returns an error to the HttpFsClient
    4.HttpFsClient displays error to the User
7. **Post-conditions**:
    - **Success:** Changes requested by user are written into file
    - **Failure:** Changes are not made and an error message is returned



## Design Patterns
Design Pattern 1: (Behavioral) Template method *RequestHandler-*[(Link)](https://github.com/httpfs/httpfs/tree/master/httpfs/server) HttpFsRequestHandler inherits from JSONRequestHandler and overrides some of the methods that it inherits.
![](https://i.imgur.com/TRnubAo.png)
Figure 5.1- UML Diagram of implementation of the Template method in the request handler classes



Design Pattern 2: (Structural) Decorator *fuse.Operations-*[(Link)](https://github.com/httpfs/httpfs/blob/master/httpfs/client/_FuseLogger.py) The fuse.Operations class is an abstract interface that enables the addition of behaviors to other classes when called during runtime.
![](https://i.imgur.com/eWmqFLv.png)
Figure 5.2- UML Diagram of implementation of the Adapter pattern in the fuse.Operation class



Design Pattern 3: (Behavioral) Strategy *CredStore-*[(Link)](https://github.com/httpfs/httpfs) The correct algorithm for the CredStore to use is selected at runtime and will choose the correct type of algorithms it needs to use.
![](https://i.imgur.com/4RY7E5I.png)
Figure 5.3-  UML Diagram of implementation of the Strategy design pattern in the CredStore classes


## Design Principles
Our design observes several of the SOLID principles.

### Single Responsibility Principle
An example of our design following the SRP is in our server.TextCredStore class. It's single responsibility is to be a repository of credentials.

### Open/closed Principle
Our HttpFsServer class follows the Open/closed principle by having all of its class variables private, making it closed to outside modification but leaves it open for extension.

### Dependency Inversion Principle
Our Authenticator and server.TextCredStore classes and our server.CredStore interface together implement the dependency inversion principle. Authenticator depends on the abstraction of a CredStore instead of the concrete implementation of a CredStore. The TextCredStore, the implementation of a CredStore, also depends on the CredStore interface, the abstraction.