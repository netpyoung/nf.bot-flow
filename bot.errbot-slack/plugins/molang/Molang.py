import textwrap
import subprocess
import git
import socket

from errbot import BotPlugin
from errbot import botcmd
from errbot import webhook

from errbot.version import VERSION
from errbot.plugin_manager import PluginConfigurationException, PluginActivationException
from rocket import Rocket
from errbot.core_plugins.wsview import bottle_app

import jenkins

# TODO(pyoung)
# description url gitlab, redmine, jenkins, hockey, admin
# gamedb
# patch

class Molang(BotPlugin):
    """
    Better than now
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        host = self.bot_config.HOST
        port = self.bot_config.PORT
        interfaces = [(host, port)]
        self.webserver = Rocket(interfaces=interfaces, app_info={'wsgi_app': bottle_app}, )
        self.webserver.start(background=True)

    @botcmd
    def echo(self, _, args):
        """
        A simple echo command.
        """
        return args

    @botcmd(split_args_with=None)
    def build_and(self, msg, args):
        """
        build_and {country} {stage}
        """
        # country, stage = args
        # r = jenkins.build_and(country, stage)
        # return str(r)
        r = jenkins.build_and('ENG', 'DEV')
        return str(r)

    @botcmd(split_args_with=None)
    def update_db(self, msg, args):
        """
        update_db
        """
        # country, stage = args
        # r = jenkins.build_and(country, stage)
        # return str(r)
        yield "start update db"
        r = jenkins.update_db('ENG', 'DEV')
        yield str(r)

    @botcmd(split_args_with=None)
    def update_locale(self, msg, args):
        """
        update_locale
        """
        # country, stage = args
        # r = jenkins.build_and(country, stage)
        # return str(r)
        yield "start update locale"
        r = jenkins.update_locale('ENG', 'DEV')
        yield str(r)

    @webhook
    def message(self, request):
        self.log.debug(repr(request))
        message = request.get('message')

        self.send(self.query_room('sb-chatop'), message)
        return "OK"

    @botcmd
    def reload(self, msg, args):
        """
        reload plugins
        """

        repo = git.Repo('.', search_parent_directories=True)
        repo.remotes.origin.pull()
        name = 'Molang'
        try:
            self._bot.plugin_manager.reload_plugin_by_name(name)
            yield "Plugin %s reloaded." % name
        except PluginActivationException as pae:
            yield 'Error activating plugin %s: %s' % (name, pae)

    @botcmd
    def help(self, msg, args):
        """
        Returns a help string listing available options.
        """

        def may_access_command(m, cmd):
            m, _, _ = self._bot._process_command_filters(
                msg=m,
                cmd=cmd,
                args=None,
                dry_run=True
            )
            return m is not None

        def get_name(named):
            return named.__name__.lower()

        # Normalize args to lowercase for ease of use
        args = args.lower() if args else ''
        usage = ''

        local_ip = socket.gethostbyname(socket.gethostname())

        description = f"""sample description"""

        cls_obj_commands = {}
        for (name, command) in self._bot.all_commands.items():
            cls = self._bot.get_plugin_class_from_method(command)
            obj = command.__self__
            _, commands = cls_obj_commands.get(cls, (None, []))
            if not self.bot_config.HIDE_RESTRICTED_COMMANDS or may_access_command(msg, name):
                commands.append((name, command))
                cls_obj_commands[cls] = (obj, commands)

        # show all
        if not args:
            for cls in sorted(cls_obj_commands.keys(), key=lambda c: cls_obj_commands[c][0].name):
                obj, commands = cls_obj_commands[cls]
                name = obj.name
                # shows class and description
                usage += '\n**{name}**\n\n*{doc}*\n\n'.format(
                    name=name,
                    doc=cls.__errdoc__.strip() or '',
                )

                for name, command in commands:
                    if command._err_command_hidden:
                        continue
                    # show individual commands
                    usage += self._cmd_help_line(name, command)
                    usage += '\n\n'  # end cls section
        elif args:
            for cls, (obj, cmds) in cls_obj_commands.items():
                if obj.name.lower() == args:
                    break
            else:
                cls, obj, cmds = None, None, None

            if cls is None:
                # Plugin not found.
                description = ''
                all_commands = dict(self._bot.all_commands)
                all_commands.update(
                    {k.replace('_', ' '): v for k, v in all_commands.items()})
                if args in all_commands:
                    usage += self._cmd_help_line(args, all_commands[args], True)
                else:
                    usage += self.MSG_HELP_UNDEFINED_COMMAND
            else:
                # filter out the commands related to this class
                description = '\n**{name}**\n\n*{doc}*\n\n'.format(
                    name=obj.name,
                    doc=cls.__errdoc__.strip() or '',
                )
                pairs = sorted([
                    (name, command)
                    for (name, command) in cmds
                    if not command._err_command_hidden and
                    (not self.bot_config.HIDE_RESTRICTED_COMMANDS or may_access_command(msg, name))
                ])

                for (name, command) in pairs:
                    usage += self._cmd_help_line(name, command)

        return ''.join(filter(None, [description, usage]))

    def _cmd_help_line(self, name, command, show_doc=False):
        """
        Returns:
            str. a single line indicating the help representation of a command.
        """
        cmd_name = name.replace('_', ' ')
        cmd_doc = textwrap.dedent(self._bot.get_doc(command)).strip()
        prefix = self._bot.prefix

        name = cmd_name
        patt = getattr(command, '_err_command_re_pattern', None)

        if patt:
            re_help_name = getattr(command, '_err_command_re_name_help', None)
            name = re_help_name if re_help_name else patt.pattern

        if not show_doc:
            cmd_doc = cmd_doc.split('\n')[0]

            if len(cmd_doc) > 80:
                cmd_doc = '{doc}...'.format(doc=cmd_doc[:77])

        help_str = '- **{prefix}{name}** - {doc}\n'.format(prefix=prefix, name=name, doc=cmd_doc)

        return help_str
