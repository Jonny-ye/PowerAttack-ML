import java.net.Socket;
import java.util.Scanner;
import java.io.PrintStream;
import java.io.FileOutputStream;
import java.io.File;
import java.io.IOException;

 public class  Client{
    Socket client;
    Scanner in;
    PrintStream out;
    public Client(){}
    public void connect(String ip, int port)throws Exception{
        this.client = new Socket(ip, port);
        this.in = new Scanner(client.getInputStream());
        this.in.useDelimiter(";");
        this.out = new PrintStream(client.getOutputStream());
        System.out.println("已连接服务器，IP地址：" + this.client.getInetAddress() + "\n");
    }
    public void close() throws Exception{
        this.out.println("exit");          //发送关闭连接指令
        this.client.shutdownInput();
        this.client.shutdownOutput();
        this.client.close();
        System.out.println("服务器断开连接");
    }
    public void receive(int time)throws Exception{       //进行一次检测过程(检测数据行数)
        File file = new File("./test_data/base.tmp");   //打开缓存文件
        if(!file.getParentFile().exists()){
            file.getParentFile().mkdirs();
        }
        if(!file.exists()){
            file.createNewFile();
        }
        PrintStream writefile = new PrintStream(new FileOutputStream(file));
        this.out.println(time);                  //发送要接收的日志的时间间隔
        if(this.in.hasNext()){                   //阻塞等待服务器发送数据
            writefile.println(this.in.next());   //输出到缓存文件
        }
    }
    
    //机器学习模型分析数据
    public String analyzeData()throws Exception{
        String cmd = "python ./src/test_pa.py";
        Runtime runtime = Runtime.getRuntime();
        Process process = runtime.exec(cmd);
        if(process.waitFor() != 0){
            System.out.println("数据计算失败");
            return null;
        }
        
        Scanner scan = new Scanner(process.getInputStream());
        scan.useDelimiter("\n");
        StringBuffer buf = new StringBuffer();
        while(scan.hasNext()){
            buf.append(scan.next());
        }
        scan.close();
        return buf.toString();
    }
    public void timer(int s)throws Exception{
        while((s--) > 0){
            System.out.printf("等待服务器搜集日志信息:%2ds\r", s);
            Thread.sleep(1000);
        }
        System.out.println("\n");
    }
    
    public static void main(String args[]){
        Client pac = new Client();
        try{
            pac.connect("localhost",5973);
            pac.timer(30);
            pac.receive(10);
            System.out.println(pac.analyzeData());
        }catch(Exception e){
            System.out.println(e);
        }finally{
            try{
                pac.close();
            }catch(Exception ex){
                System.out.println(ex);
            }
        }
    }
}
 
