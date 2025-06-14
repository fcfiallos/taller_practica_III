from hdfs import InsecureClient

class HDFSClient:
    def __init__(self, namenode_url):
        self.client = InsecureClient(namenode_url, user="root", timeout=30)
        for d in ["/uploads"]:
            if not self.client.status(d, strict=False):
                self.client.makedirs(d)

    def save_file(self, hdfs_path, local_path):
        return self.client.upload(hdfs_path, local_path, overwrite=True)

    def read_file(self, hdfs_path):
        with self.client.read(hdfs_path) as reader:
            return reader.read()