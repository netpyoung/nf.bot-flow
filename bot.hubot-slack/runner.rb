#!/usr/bin/ruby
$stdout.sync = true
require 'net/http'
require 'rake'

ENV['HUBOT_SLACK_TOKEN'] = 'BLABLA_HUBOT_SLACK_TOKEN'
ENV['PORT'] = '8888'
CMD_BOTRUNNER = 'bin/hubot -a slack'

Dir.chdir('.') do
  while true
    begin
      sh "#{CMD_BOTRUNNER}"
    rescue Exception => e
      puts e
    end
  end
end
