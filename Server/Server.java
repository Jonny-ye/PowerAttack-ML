
import java.net.Socket;
import java.net.ServerSocket;
import java.util.List;
import java.util.ArrayList;
import java.util.Scanner;
import java.io.File;
import java.io.IOException;
import java.io.PrintStream;
import java.io.RandomAccessFile;

//自定义文件工具类
class JyFile{

    //数据行反转拼接
    public static StringBuffer reverseLines(List<String> list){
        StringBuffer buf = new StringBuffer();
        for(int i=list.size()-1; i>=0; i--){
            buf.append((String)list.get(i));
            buf.append("\n");
        }
        buf.append(";");
        return buf;
    }
    
    //读取文件最后N行
    public static List<String> readLastNLine(File file, int numRead){
        List<String> result = new ArrayList<String>();
        try{
            RandomAccessFile fileRead = new RandomAccessFile(file, "r");
            long pos = fileRead.length() - 1;
            int count = 0;
            while (pos >= 0){
                pos--;
                fileRead.seek(pos);
                if (fileRead.readByte() == '\n'){
                    result.add(fileRead.readLine());
                    if (++count == numRead){
                        break;
                    }
                }
            }
            fileRead.close();
        }catch (IOException e){
            e.printStackTrace();
        }
        return result;
    }
}

//客户端线程
class ClientThread implements Runnable{
    private Socket client;
    public ClientThread(Socket client){
        this.client = client;
    }
    public void run(){
        try{
            System.out.println(Thread.currentThread() + "：客户端连接");
            Scanner in = new Scanner(this.client.getInputStream());
            in.useDelimiter("\n");
            PrintStream out = new PrintStream(this.client.getOutputStream());
            
            while(true){
                if(in.hasNext()){
                    String data = in.next().trim();
                    if("exit".equalsIgnoreCase(data)){
                        break;
                    }else{
                        String location = "./data/base.log";  //日志文件位置
                        int row = Integer.valueOf(data);
                        if(row>=10 && row<=50){      //判断行数合法性 
                            List<String> list = JyFile.readLastNLine(new File(location), row); 
                            StringBuffer buf = JyFile.reverseLines(list);
                            out.println(buf.toString());
                            System.out.println(Thread.currentThread() + "：向客户端发送数据");
                        }
                    }//else
                }else{
                   break;
                }
            }
            this.client.shutdownInput();
            this.client.shutdownOutput();
        }catch(Exception e){
            e.printStackTrace();
        }finally{
            try {
                this.client.close();
                System.out.println(Thread.currentThread() + "：客户端断开连接");
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }//run()
}

public class Server{
    public static void main(String[] args){
        try{
            Runtime runtime = Runtime.getRuntime();
            runtime.exec("./log_service.sh &");
            ServerSocket server = new ServerSocket(5973);     //启用端口
            System.out.println("服务器监控服务启动，端口：" + server.getLocalPort() + "\n");
            
            //等待客户端连接
            boolean flag=true;
            while(flag){
                Socket client = server.accept();
                new Thread(new ClientThread(client)).start();
            }
            server.close();
        }catch(Exception e){
            e.printStackTrace();
        }
    }
}
