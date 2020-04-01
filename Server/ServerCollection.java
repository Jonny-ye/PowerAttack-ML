
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Scanner;
import java.io.File;
import java.io.IOException;
import java.io.PrintStream;
import java.io.RandomAccessFile;

//System.currenTimeMillis()
//读取文件
class ReadFile{
    public static StringBuffer readLastNLine(File file, long numRead){
        StringBuffer buf = new StringBuffer();
        if (!file.exists() || file.isDirectory() || !file.canRead()){
            return null;
        }
        try{
            long count = 0;
            RandomAccessFile fileRead = new RandomAccessFile(file, "r");
            long length = fileRead.length();
            if (length == 0L){
                return buf;
            }else{
                long pos = length - 1;
                while (pos > 0){
                    pos--;
                    fileRead.seek(pos);
                    if (fileRead.readByte() == '\n'){
                        buf.append(fileRead.readLine());
                        if (++count == numRead){
                            buf.append(";");
                            break;
                        }else{
                            buf.append("\n");
                        }
                    }
                }
                if (pos == 0)
                {
                    fileRead.seek(0);
                    buf.append(fileRead.readLine());
                }
            }
            fileRead.close();
        }
        catch (IOException e){
            e.printStackTrace();
        }
        return buf;
    }
}

//客户端线程
class MyThread implements Runnable{
    private Socket client;
    public MyThread(Socket client){
        this.client = client;
    }
    public void run(){
        try{
            Scanner in = new Scanner(this.client.getInputStream());
            in.useDelimiter("\n");
            PrintStream out = new PrintStream(this.client.getOutputStream());
            boolean flag = true;
            while(flag){
                if(in.hasNext()){
                    String data = in.next().trim();
                    if("exit".equalsIgnoreCase(data)){
                        flag = false;
                        out.println("断开链接");
                        break;
                    }else if("need_data".equals(data)){
                        String location = "./log_data/base_data.log";
                        StringBuffer buf = ReadFile.readLastNLine(new File(location),20L);
                        out.println(buf.toString());
                    }
                }
            }
            this.client.shutdownInput();
            this.client.shutdownOutput();
        }catch(Exception e){
            e.printStackTrace();
        }finally{
            try {
                client.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

}
public class ServerCollection{
    public static void main(String[] args){
        try{
            Runtime runtime = Runtime.getRuntime();
            Process p = runtime.exec("./log_service.sh &");
            System.out.println("日志采集子进程启动...");
            ServerSocket server = new ServerSocket(5210);     //启用端口
            System.out.println("服务器监控主进程启动...");
            //等待客户端链接
            boolean flag = true;
            while(flag){
                Socket client = server.accept();              //等待客户端链接
                new Thread(new MyThread(client)).start();
            }
            server.close();
        }catch(Exception e){
            e.printStackTrace();
        }
    }
} 
 
 
