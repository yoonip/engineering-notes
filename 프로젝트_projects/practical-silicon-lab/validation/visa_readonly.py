#!/usr/bin/env python3
"""Real PyVISA transport template. Only identification is sent by this example."""
import argparse
import json
import time


class VisaTransport:
    def __init__(self, resource, termination='\n', backend=None):
        import pyvisa  # Optional dependency; the local model needs no PyVISA.
        self.manager = (pyvisa.ResourceManager(backend) if backend
                        else pyvisa.ResourceManager())
        self.device = None
        try:
            self.device = self.manager.open_resource(resource)
            self.device.timeout = 2000  # VISA timeout uses milliseconds.
            self.device.read_termination = termination  # Check the manual.
            self.device.write_termination = termination
        except Exception:
            # Initialization can fail before main() reaches its finally.
            self.close()
            raise
        self.log = []

    def query(self, command):
        # Keeping the command explicit prevents a fake universal instrument API.
        began = time.monotonic()
        response = self.device.query(command).strip()
        self.log.append({'command': command, 'response': response,
                         'host_elapsed_s': time.monotonic() - began})
        return response

    def close(self):
        try:
            if self.device is not None:
                self.device.close()
        finally:
            self.manager.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--resource', required=True,
                        help='Exact VISA resource from the instrument inventory')
    parser.add_argument('--backend', default=None,
                        help='For example @py if pyvisa-py is installed')
    args = parser.parse_args()
    transport = VisaTransport(args.resource, backend=args.backend)
    try:
        # Do not send *RST, OUTP ON, or guessed voltage commands to an unknown box.
        print(transport.query('*IDN?'))
        print(json.dumps(transport.log, indent=2))
    finally:
        transport.close()
