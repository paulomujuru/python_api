
You can install Docker by following this [link](https://www.docker.com/get-started)

Once docker is installed you will require Docker Compose (for Windows users this comes preinsatlled with Docker).

### Linux

Install Compose on Linux systems
On Linux, you can download the Docker Compose binary from the Compose repository release page on GitHub. Follow the instructions from the link, which involve running the curl command in your terminal to download the binaries. These step-by-step instructions are also included below.

```bash
For alpine, the following dependency packages are needed: py-pip, python-dev, libffi-dev, openssl-dev, gcc, libc-dev, and make.
```

Run this command to download the current stable release of Docker Compose:

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

Apply executable permissions to the binary:

```bash
sudo chmod +x /usr/local/bin/docker-compose
```
Note: If the command docker-compose fails after installation, check your path. You can also create a symbolic link to /usr/bin or any other directory in your path.


For example:

```bash
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
```
Optionally, install command completion for the bash and zsh shell.

Test the installation.

```bash
$ docker-compose --version
docker-compose version 1.27.4, build 1110ad01
```

# Usage

## Linux

```bash
sudo docker-compose build

```
```bash
sudo docker-compose up

```


## Windows

```bash
docker-compose build

```
```bash
docker-compose up

```


If no errors have occured than you should be able access the API on

http://localhost:5000



# ***API Example Requests***

## Register a User

## Endpoint: http://localhost:5000/user/register
## Method: POST
## Headers: 

```bash
{
    "Content-Type": "application/json"
}
```
## Body:
```bash
{
    "username": "Test",
    "password": "12345678"
}
```

## Reponse Code: 200
## Reponse:
```bash
{
  "Message": "User Registered Successfully",
  "data": {
    "username": "Test",
    "password": "gAAAAABgCrmkZxY39eeSodYrItOVx47wgza37ty-6fDTb-5L_dLufmNvFuLK8DqYLBdN7mdmenFV2G1LcB6cdqUvadfRxCmxjA=="
  }
}
```


## Login a User

## Endpoint: http://localhost:5000/user/register
## Method: POST
## Headers: 

```bash
{
    "Content-Type": "application/json"
    "Autherization": "Basic {username:password}"
}
```
## Body:
```bash
{
    "username": "Test",
    "password": "12345678"
}
```

## Reponse Code: 200
## Reponse:
```bash
{
  "Message": "Login Successful"
}
```
## Create a profile

## Endpoint: http://localhost:5000/edit/profiles
## Method: POST
## Headers: 

```bash
{
    "Content-Type": "application/json"
    "Autherization": "Basic {username:password}"
}
```
## Body:
```bash
{
    "name": "Test",
    "age": "12",
    "favourite_color": "Pink",
    "favourite_OS": "Ubuntu" 
}
```

## Reponse Code: 200
## Reponse:
```bash
{
  "data": [
    "Test",
    "12",
    "Pink",
    "Ubuntu"
  ]
}
```
## Search Profiles
## Method: POST
## Endpoint: http://localhost:5000/search/profiles
## Headers: 

```bash
{
    "Content-Type": "application/json"
    "Autherization": "Basic {username:password}"
}
```
## Body:
```bash
{
	"profileid": 2
}
```

## Reponse Code: 200
## Reponse:
```bash
{
  "data": {
    "name": "Test",
    "age": "12",
    "favourite_color": "Pink",
    "favourite_OS": "Ubuntu"
  }
}
```

## Edit Profile

## Endpoint: http://localhost:5000/edit/profiles
## Method: PUT
## Headers: 

```bash
{
    "Content-Type": "application/json"
    "Autherization": "Basic {username:password}"
}
```
## Body:
```bash
{
	"profileid": 2,
    "name": "foo"
}
```

## Reponse Code: 200
## Reponse:
```bash
{
  "data": {
    "name": "foo",
    "age": "12",
    "favourite_color": "Pink",
    "favourite_OS": "Ubuntu"
  }
}
```

