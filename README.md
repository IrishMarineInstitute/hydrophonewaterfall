# hydrophonewaterfall
hydrophone waterfall plotting service

Application to fetch hydrophone data from spiddal.marine.ie and graph.

(This is a work in progress)

    docker build -t marine/hydrophonewaterfall .
    docker run -d --name hydrophonewaterfall -p 80:80 marine/hydrophonewaterfall

After about 30 seconds you should be able to get some data from web service.

    curl -o pic.png localhost


