server {
        listen 80;
        server_name static.designserviceusa.com;

        access_log /home/bjones/projects/dsusa/var/log/www.access.log;
        error_log /home/bjones/projects/dsusa/var/log/www.error.log error;

        location / {
                root /home/bjones/projects/dsusa/com_designserviceusa/static;
                index index.html;
        }
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
                root   /var/www/nginx-default;
        }
}

server {
	listen 80;
	server_name stage.designserviceusa.com;

	access_log /home/bjones/projects/dsusa/var/log/www.access.log;
	error_log /home/bjones/projects/dsusa/var/log/www.error.log error;

	location / {
		fastcgi_pass djangositeserv;
		fastcgi_param PATH_INFO $fastcgi_script_name;
		fastcgi_param REQUEST_METHOD $request_method;
		fastcgi_param QUERY_STRING $query_string;
		fastcgi_param CONTENT_TYPE $content_type;
		fastcgi_param CONTENT_LENGTH $content_length;
		fastcgi_param  SERVER_PROTOCOL    $server_protocol;
		fastcgi_param  SERVER_NAME $server_name;
		fastcgi_param  SERVER_PORT        $server_port;
		fastcgi_pass_header Authorization;
		fastcgi_intercept_errors off;
	}
}
