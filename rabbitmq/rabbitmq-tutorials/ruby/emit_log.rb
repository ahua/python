#!/usr/bin/env ruby
# encoding: utf-8

require "amqp"

AMQP.start(:host => "localhost") do |connection|
  channel  = AMQP::Channel.new(connection)
  exchange = channel.fanout("logs")
  message  = ARGV.empty? ? "info: Hello World!" : ARGV.join(" ")

  exchange.publish(message)
  puts " [x] Sent #{message}"

  EM.add_timer(0.5) do
    connection.close do
      EM.stop { exit }
    end
  end
end
