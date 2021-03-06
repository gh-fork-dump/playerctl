import asyncio


class CommandResult:
    def __init__(self, stdout, stderr, returncode):
        self.stdout = stdout.decode().strip()
        self.stderr = stderr.decode().strip()
        self.returncode = returncode


class PlayerctlCli:
    def __init__(self, bus_address=None):
        self.bus_address = bus_address

    async def run(self, cmd):
        shell_cmd = f'playerctl {cmd}'

        if self.bus_address:
            shell_cmd = f'DBUS_SESSION_BUS_ADDRESS={self.bus_address} {shell_cmd}'

        proc = await asyncio.create_subprocess_shell(
            shell_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await proc.communicate()
        await proc.wait()
        return CommandResult(stdout, stderr, proc.returncode)
