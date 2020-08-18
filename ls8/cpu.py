"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0]*128
        self.reg = [0]*128
        self.running = False
        self.pc = 0
        self.HLT = 0b00000001
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.ADD = 0b10100000
        self.SUB = 0b10100001
        self.MUL = 0b10100010
        self.DIV = 0b10100011
        self.ALU = [self.ADD, self.SUB, self.MUL, self.DIV]

    def load(self, filename):
        """Load a program into memory."""
        try:
            address = 0
            with open(filename) as f:
                for line in f:
                    comment_split = line.split("#")
                    n = comment_split[0].strip()

                    if n == '':
                        continue

                    val = int(n, 2)
                    # store val in memory
                    self.ram[address] = val

                    address += 1

                    # print(f"{x:08b}: {x:d}")

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {filename} not found")
            sys.exit(2)

        # address = 0

        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == self.ADD:
            self.reg[reg_a] += self.reg[reg_b]
        elif op == self.SUB:
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == self.MUL:
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == self.DIV:
            self.reg[reg_a] /= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, adress):
        return self.ram[adress]

    def ram_write(self, adress, value):
        self.ram[adress] = value

    def run(self):
        """Run the CPU."""
        self.running = True
        while self.running:
            cmd = self.ram[self.pc]

            if cmd == self.HLT:
                self.running = False
                op_size = 1

            elif cmd == self.LDI:
                reg_index = self.ram[self.pc+1]
                value = self.ram[self.pc+2]

                self.reg[reg_index] = value

                op_size = 3

            elif cmd == self.PRN:
                reg_index = self.ram[self.pc+1]
                value = self.reg[reg_index]
                print(value)

                op_size = 2

            elif cmd in self.ALU:
                reg_index_a = self.ram[self.pc+1]
                reg_index_b = self.ram[self.pc+2]
                print(self.reg[reg_index_a], self.reg[reg_index_b])
                self.alu(cmd, reg_index_a, reg_index_b)

                op_size = 3

            self.pc += op_size
