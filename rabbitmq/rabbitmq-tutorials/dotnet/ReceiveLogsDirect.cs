using System;
using RabbitMQ.Client;
using RabbitMQ.Client.Events;

class ReceiveLogsDirect {
    public static void Main(string[] args) {
        ConnectionFactory factory = new ConnectionFactory();
        factory.HostName = "localhost";
        using (IConnection connection = factory.CreateConnection())
        using (IModel channel = connection.CreateModel()) {

            channel.ExchangeDeclare("direct_logs", "direct");
            string queue_name = channel.QueueDeclare();

            if (args.Length < 1) {
                Console.Error.WriteLine("Usage: {0} [info] [warning] [error]",
                                        Environment.GetCommandLineArgs()[0]);
                Environment.ExitCode = 1;
                return;
            }

            foreach (string severity in args) {
                channel.QueueBind(queue_name, "direct_logs", severity);
            }

            Console.WriteLine(" [*] Waiting for messages. " +
                              "To exit press CTRL+C");

            QueueingBasicConsumer consumer = new QueueingBasicConsumer(channel);
            channel.BasicConsume(queue_name, true, consumer);

            while(true) {
                BasicDeliverEventArgs ea =
                    (BasicDeliverEventArgs)consumer.Queue.Dequeue();

                byte[] body = ea.Body;
                string message = System.Text.Encoding.UTF8.GetString(body);
                string routingKey = ea.RoutingKey;
                Console.WriteLine(" [x] Received '{0}':'{1}'",
                                  routingKey, message);
            }
        }
    }
}
