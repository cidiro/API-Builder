# env.sample.py
# env.sample builder

def build(entities):
    return "MONGO_URL=mongodb://[username:password@]host1[:port1][,host2[:port2],...[,hostN[:portN]]][/[database][?options]]\n"
