# How to render the checklist

This is a quick "how to" to render the checklist. If you want details on implementation, scroll down to the relevant section below

## How to

-   Clone the schema user interface [forked repository](https://github.com/Remi-Gau/cobidas-ui)
-   Step inside the schema-ui directory, checkout the COBIDAS development branch and install the dependencies

```
git clone https://github.com/Remi-Gau/cobidas-ui
cd schema-ui
git checkout COBIDAS
```

### Run Locally

-   Install [npm](https://www.npmjs.com/get-npm) or better install [node version manager](https://github.com/nvm-sh/nvm) to help you deal with different version of node.js.

If you are running linux go for:

`curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.11/install.sh | bash`

Then close your terminal and reopen it then run

```
nvm install node
nvm install 9
```

-   Step inside the `cobidas-ui` directory and install the dependencies
-   Run the development server
```
npm install
npm run dev
```

-   Open your browser and go to [localhost:8080](localhost:8080)


### Run with docker or docker-compose

If you are new to docker you might want to check [this](https://the-turing-way.netlify.com/reproducible_environments/06/containers#Containers_section) first.

Maybe more, please check

```
this_dir=`pwd`
docker build -t cobidas-checklist:0.0.1 .
docker run -it --rm -p 8080:8080 -v $this_dir:/code cobidas-checklist:0.0.1
```

To make things easier, can can also use [docker-compose](https://docs.docker.com/compose), which load the docker configuration from the `docker-compose.yml` file. In that case, the only things you need to do is to run:

```
docker-compose up
```
Then open your browser and go to [http://0.0.0.0:8080/](http://0.0.0.0:8080/) or [localhost:8080/](localhost:8080/)

[@TimVanMourik](https://github.com/TimVanMourik) dockerised this app in [this PR](https://github.com/Remi-Gau/cobidas-ui/pull/2).


## Implementation

Just some quick details on how the rendering is done at the moment.

This relies on the schema-ui repository [forked here for development](https://github.com/Remi-Gau/cobidas-ui): the work is done on the COBIDAS branch of this repo, so make sure you checkout this branch before you decide to serve the checklist.

The server-ui can be used to render different questionnaires following the [schema-standardization work](https://github.com/ReproNim/schema-standardization) done by ReproNim. For the purpose of development, this repository was also forked [here](https://github.com/Remi-Gau/schema-standardization). There too the dev work is done on the COBIDAS branch.

### In practice

Server-ui can be set to get info from another repo by modifying its `schema-ui/src/config.js` file (e.g see [here](https://github.com/Remi-Gau/cobidas-ui/blob/COBIDAS/src/config.js)).

A cobidas activity set was created in the schema-standardization repo in the folder `schema-standardization/activity-sets/cobidas`.

This points to the cobidas activity defined in `schema-standardization/activities/COBIDAS` where the items of the checklist are themselves defined.