#!/usr/bin/python
# encoding=utf8

'''
Created on May 2, 2012
远程过程调用服务器RPCServer
@author: Lee Guojun
@功能:1.消息队列分派器，等待来自judgeClient的请求，每来一个请求，就从相应的队列中取出提交消息并
传给judgeClient，等到收到来自judgeClient的完成相应时就发给judgeServer一个对应的ACK，然后judgeServer
才可以从队列中把这个消息free掉。
2.收集来自JudgeClient的处理结果，并把它写到数据库中。

@性质:1.JudgeServer的RPCServer。2.RabbitMQClient。
'''
from sdust_oj.sa_conn import Session
from sdust_oj.status import *
from SimpleXMLRPCServer import SimpleXMLRPCServer,SimpleXMLRPCRequestHandler        # \
from SocketServer import ForkingMixIn   
from sdust_oj.tables.auth import User                                            # | RPCServer 
from sdust_oj.tables.problem import Submission,Problem
import sys      
import pika     # rabbitMQ 链接库
import pickle

UNABLE_TO_CONNECT = 1
UNABLE_TO_GET_CHANNEL = 2
OnLineJudgeStatus = ["Pending","Keyword_checking","Compiling","Running","Output_checking"]
EndStatus =[keyword_checked_error,compiled_error,compiled_error,runtime_error,memory_over_error,presentation_error,fetched]

class RPCServer:
    connection = None
    channel = None
    flag = False
    host = "http://localhost"
    port = 8765
    serveraddr = (host,port)
    
    """
    一下几个函数是相对于RabbitMQ来说，是客户端
    """
    def getConnection(self,host="localhost"):
        """
        链接RabiitMQ，获得connection
        """
        self.host = host
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
            self.flag = True
        except Exception as e:
            print "Unable to Connect RabbitMQ"
            print e
        return self.flag
    
    def getChannel(self):
        """
        获得channel
        """
        try:
            self.channel = self.connection.channel()
        except Exception as e:
            print "Unable to get RabbitMQ channel "
            print e
            
    def __init__(self,host="localhost"):
        """
        初始化就保持与RabbitMQ的链接，一直到服务器停止，若链接不上，则停止程序运行
        """
        if self.getConnection(host) == False:
            sys.exit(UNABLE_TO_CONNECT)
        self.getChannel()
    
    def bindByStatus(self,status=None):
        que = status + "_queue"
        exc = status + "_exchange"
        #在这里又重新声明了队列是因为RabbitMQ的server端和client端不知道谁先运行
        self.channel.queue_declare(queue=que,               
                        durable=True,                    
                        exclusive=False,                
                        auto_delete=False,                
                        )
        self.channel.exchange_declare(exchange=exc,		
						type="direct",
						durable=True,
						auto_delete=False,
						)
        self.channel.queue_bind(queue=que,                    
                        exchange=exc,                   
                        routing_key=status,                
                        )

    
    def bind(self):
        for status in OnLineJudgeStatus:
            self.bindByStatus(status)
    
    def onRequest(self,status):
        """
        这是提供给RPClient的接口,根据状态返回请求
        eg： onRequest("Pending") or onRequest("Compiling")
        """
        print status
        print 1
        que = status + "_queue"
        method_frame, header_frame, body = self.channel.basic_get(queue=que)
        if method_frame.NAME == 'Basic.GetEmpty':
            print 'Receive empty message.'
        else:
            print 2
            print body
            print 'body=%s,method_frame=%s,header_frame=%s'%(body,method_frame.delivery_tag,header_frame)
            self.channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        return body # message(submission)

    def updateStatusById(self, sid, status):
        """
        根据ID更新提交的状态
        """
        session = self.getSession()    
        print "tag1"
        s = session.query(Submission).get(int(sid))
        print "tag2"
        s.status = int(status)
        session.commit()
        print "tag3"
        self.closeSession(session)
        print "update id:%s to status:%s success!" % (sid, status)
        
    def updateStatusAndMTById(self, sid, status, mm, tt):
        """
        根据ID更新提交的状态
        """
        session = self.getSession()    
        print "tag1"
        s = session.query(Submission).get(int(sid))
        print "tag2"
        s.status = int(status)
        s.used_memory = mm
        s.used_time = tt
        session.commit()
        print "tag3"
        self.closeSession(session)
        print "update id:%s to status:%s success!" % (sid, status)

    def getSubmissionById(self,mid):
        """
        根据id获得这个对象
        """
        session = self.getSession()    
        session.expire_on_commit = False
        message = []
        try:
            message = session.query(Submission).get(int(mid))
            print 'message.id=%d'%message.id
            b = pickle.dumps(message)
        except Exception as e:
            print "Exception raised in handleCompilingById()"
            print e    
        self.closeSession(session)
        return  b

    def getMetaIOByID(self, mid):
        session = self.getSession()
        problem = session.query(Problem).join(Submission).filter(Submission.id == mid).first()
        meta_id = problem.problem_meta_id
        io_list = []
        for io in problem.input_output_datas:
                io_list.append(io.id)
        self.closeSession(session)
        return meta_id, io_list
        
    def helloworld(self):
		return 'hello world'
    def getSession(self):
        """
        或得数据库session
        """
        try:
            session = Session()    # 开启与数据库的链接
        except Exception as e:
            print "Open Session Error"
            print e
        return session
        
    def closeSession(self,session):
        try:
            session.close()        # 关闭与数据库的链接
        except Exception as e:
            print "Session close Error"
            print e
    
    def sendBack(self,message):
        session = self.getSession()
        session.add(message)
        session.dirty
        session.commit()
        self.closeSession(session)
        return None
    
class ForkingServer(ForkingMixIn,SimpleXMLRPCServer):
    pass
def test():
    if __name__  == '__main__':
        serveraddr =('localhost',8765)
        server = ForkingServer(serveraddr,SimpleXMLRPCRequestHandler)
        server.register_multicall_functions()
        server.register_instance(RPCServer())
        server.register_introspection_functions()
        print "[x] Waiting ..."
        server.serve_forever()
    else:
        print __name__ + "Called by JudgeServer..."
def main():

    serveraddr =('localhost',8765)
    server = ForkingServer(serveraddr,SimpleXMLRPCRequestHandler,allow_none=True)
    server.register_multicall_functions()
    server.register_instance(RPCServer())
    server.register_introspection_functions()
    print "[x] Waiting ..."
    server.serve_forever()



