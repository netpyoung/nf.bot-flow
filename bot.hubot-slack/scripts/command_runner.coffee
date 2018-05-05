# Description:
#    command_runner

fs = require('fs')
spawn = require('child_process').spawn
spawnSync = require('child_process').spawnSync
encoding = require('encoding')
{split} = require('shellwords')
chdir = require('chdir')
path = require('path')


SCRIPT_DIR = 'commands'
is_windows = /^win/.test(process.platform)
room = {room: 'chatops'}

tr = (message) ->
  if is_windows
    return encoding.convert(message, 'UTF-8', 'EUC-KR')
  else
    return message

gen_spawn = (msg) ->
  if is_windows
    cmd = msg.match[1]
    args = msg.match[2]
    return spawn('cmd', ['/s', '/c', "#{path.resolve(SCRIPT_DIR, cmd)} #{args}"])
  else
    cmd = msg.match[1]
    args = split(msg.match[2])
    return spawn(path.resolve(SCRIPT_DIR, cmd), args)



module.exports = (robot) ->
  robot.hear /^!reload/, (msg) ->
    msg.send('[START] script update')
    chdir SCRIPT_DIR, () ->
      ps = spawnSync('git', ['pull'])
      msg.send """
#{tr(ps.stdout)}
loaded script : #{fs.readdirSync('.')}
"""
    msg.send('[DONE] script update')


  robot.hear /^!([a-z|A-Z]*)(.*)/, (msg) ->
    cmd = msg.match[1]
    if (cmd == null)
      return
    if (cmd == 'reload')
      return

    child = gen_spawn(msg)
    child.on 'error', (err) ->
      msg.send("#{err}")
    child.stdout.on 'data', (data) ->
      msg.send(data.toString())
    child.stderr.on 'data', (data) ->
      msg.send('[ERROR]: #{tr(data)}')


  robot.router.post '/hubot/say', (req, res) ->
    message = req.body.message
    robot.send(room, message)
    res.writeHead(200, {'Content-Type': 'text/plain'})
    res.end '\n'
