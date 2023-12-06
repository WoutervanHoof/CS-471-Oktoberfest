file = "trace.out"
pid = "python-1450"

class Function:
    # page_fault_user: address=0x7f390c54dedc ip=0x7f390cd06a2c error_code=0x4
    kind: str
    address: str
    ip: str
    error_code: str

    @staticmethod
    def from_string(string):
        # split string into columns
        columns = string.split()

        # create function
        f = Function()
        f.kind = columns[0][:-1]
        f.address = columns[1].split("=")[1]
        f.ip = columns[2].split("=")[1]
        f.error_code = columns[3].split("=")[1]

        return f
    
    def __str__(self):
        return f"{self.kind} {self.address} {self.ip} {self.error_code}"

class Datapoint:
    task_pid: str
    cpu: int
    irqs_off: str
    need_resched: str
    hardirqs_off: str
    preempt_count: str
    migration_disabled: str

    timestamp: str
    function: Function
    function_str: str

data = []
with open(file, "r") as f:
    # ignore lines that start with #
    for line in f:
        if line[0] == "#":
            continue

        # split line into columns
        columns = line.split()

        # create datapoint
        dp = Datapoint()
        dp.task_pid = columns[0]
        
        # the cpu is [001]
        dp.cpu = int(columns[1][1:-1])

        # the 2nd column are all flags
        dp.irqs_off = columns[2][0]
        dp.need_resched = columns[2][1]
        dp.hardirqs_off = columns[2][2]
        dp.preempt_count = columns[2][3]
        dp.migration_disabled = columns[2][4]

        # the 3rd column is the timestamp
        dp.timestamp = columns[3]

        # the reamining columns are the function
        dp.function_str = " ".join(columns[4:])

        # add datapoint to data
        data.append(dp)

# filter only for datapoints with the given pid (part of task_pid)
data = list(filter(lambda dp: pid in dp.task_pid, data))

# convert function column to Function object
for dp in data:
    dp.function = Function.from_string(dp.function_str)


# categorize datapoints by error_code
datapoints_by_error_code = {}
for dp in data:
    if dp.function.error_code not in datapoints_by_error_code:
        datapoints_by_error_code[dp.function.error_code] = []
    datapoints_by_error_code[dp.function.error_code].append(dp)

# print datapoints_by_error_code count
for error_code, datapoints in datapoints_by_error_code.items():
    print(f"{error_code}: {len(datapoints)}")        


# given that 0x14 are page faults, let's filter for those
page_fault_datapoints = datapoints_by_error_code["0x14"]

# can we find a pattern in the page faults?
# let's look at the addresses
page_fault_addresses = [dp.function.address for dp in page_fault_datapoints]
