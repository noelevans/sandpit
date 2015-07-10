print(".")
print(commandArgs(trailingOnly=TRUE))
print(".")
print(length(commandArgs(trailingOnly=TRUE)))
print(".")
if("--full" %in% commandArgs(trailingOnly=TRUE)) {
    print("Responding to true arg on command line")
} else {
    print('Have not registered "--full" arg')
}