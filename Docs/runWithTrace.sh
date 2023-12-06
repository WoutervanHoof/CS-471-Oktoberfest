#!/bin/bash

# Default values
TRACE_OUTPUT="trace.out"
COMMAND_OUTPUT=""
COMMAND=""

# Parsing command line arguments
for i in "$@"
do
case $i in
    --trace-output=*)
    TRACE_OUTPUT="${i#*=}"
    shift
    ;;
    --command-output=*)
    COMMAND_OUTPUT="${i#*=}"
    shift
    ;;
    --command=*)
    COMMAND="${i#*=}"
    shift
    ;;
    *)
    # unknown option
    ;;
esac
done

# Check if a command is provided
if [ -z "$COMMAND" ]; then
    echo "No command provided to execute."
    exit 1
fi

# Check if FTRACE is enabled
zcat /proc/config.gz | grep FTRACE
if [ $? -ne 0 ]; then
    echo "FTRACE is not enabled. Recompile with debugging enabled."
    exit 1
fi

# Enable page_fault_user tracepoint
echo page_fault_user > /sys/kernel/debug/tracing/set_event

# Start tracing
echo 1 > /sys/kernel/debug/tracing/tracing_on

# Execute the command with or without output redirection
if [ -z "$COMMAND_OUTPUT" ]; then
    eval $COMMAND
else
    eval $COMMAND > "$COMMAND_OUTPUT"
fi

# Stop tracing
echo 0 > /sys/kernel/debug/tracing/tracing_on

# Save the trace output
cat /sys/kernel/debug/tracing/trace > "$TRACE_OUTPUT"
