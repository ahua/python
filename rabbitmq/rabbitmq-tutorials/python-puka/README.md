# Python-Puka code for RabbitMQ tutorials

Here you can find code examples from
[RabbitMQ tutorials](http://www.rabbitmq.com/getstarted.html) adapted
to [Puka](https://github.com/majek/puka) Python library.


## Requirements

Now you can install `puka` using Pip:

      pip install puka

You may need to install `pip` first:

  * On Ubuntu:

        sudo apt-get install python-pip

  * On Debian:

        sudo apt-get install python-setuptools
        sudo easy_install pip


## Code

[Tutorial one: "Hello World!"](http://www.rabbitmq.com/tutorial-one-python.html):

    python send.py
    python receive.py

[Tutorial two: Work Queues](http://www.rabbitmq.com/tutorial-two-python.html):

    python new_task.py
    python worker.py

[Tutorial three: Publish/Subscribe](http://www.rabbitmq.com/tutorial-three-python.html):

    python receive_logs.py
    python emit_log.py

[Tutorial four: Routing](http://www.rabbitmq.com/tutorial-four-python.html):

    python receive_logs_direct.py
    python emit_log_direct.py

[Tutorial five: Topics](http://www.rabbitmq.com/tutorial-five-python.html):

    python receive_logs_topic.py
    python emit_log_topic.py

[Tutorial six: RPC](http://www.rabbitmq.com/tutorial-six-python.html):

    python rpc_server.py
    python rpc_client.py
