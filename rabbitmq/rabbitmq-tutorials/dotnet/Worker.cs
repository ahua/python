using System;
using RabbitMQ.Client;
using RabbitMQ.Client.Events;

class Worker {
    public static void Main() {
        ConnectionFactory factory = new ConnectionFactory();
        factory.HostName = "localhost";
        using (IConnection connection = factory.CreateConnection())
        using (IModel channel = connection.CreateModel()) {
            channel.QueueDeclare("task_queue", true, false, false, null);

            channel.BasicQos(0, 1, false);
            QueueingBasicConsumer consumer = new QueueingBasicConsumer(channel);
            channel.BasicConsume("task_queue", false, consumer);

            Console.WriteLine(" [*] Waiting for messages. " +
                              "To exit press CTRL+C");
            while(true) {
                BasicDeliverEventArgs ea =
                    (BasicDeliverEventArgs)consumer.Queue.Dequeue();

                byte[] body = ea.Body;
                string message = System.Text.Encoding.UTF8.GetString(body);
                Console.WriteLine(" [x] Received {0}", message);

                int dots = message.Split('.').Length - 1;
                System.Threading.Thread.Sleep(dots * 1000);

                Console.WriteLine(" [x] Done");

                channel.BasicAck(ea.DeliveryTag, false);
            }
        }
    }
}
