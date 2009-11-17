server {
	listen 80;
	server_name stage.designserviceusa.com;

        access_log /var/log/nginx/com_designserviceusa_stage-access.log;
        error_log /var/log/nginx/com_designserviceusa_stage-error.log error;

	location ~ /(css|img|js|pic)/ {
		root /var/www/com_designserviceusa_stage/static;
	}

	location / {
		fastcgi_pass unix:/var/www/com_designserviceusa_stage/var/website-fcgi.sock;
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

        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
                root   /var/www/nginx-default;
        }
}
