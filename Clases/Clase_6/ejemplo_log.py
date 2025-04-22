with open('/tmp/log_fifo', 'r') as fifo, open('registro.log', 'a') as log:
    for line in fifo:
        log.write(line)