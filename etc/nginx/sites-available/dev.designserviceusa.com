server {
	listen 80;
	server_name dev-static.designserviceusa.com;
	
	access_log /home/bjones/projects/dsusa/var/log/dev-static.access.log;
	error_log /home/bjones/projects/dsusa/var/log/dev-static.error.log error;

	location / {
		root /home/bjones/projects/dsusa/designfirst-static;
	}
}

server {
	listen 80;
	server_name dev.designserviceusa.com;

	access_log /home/bjones/projects/dsusa/var/log/dev.access.log;
	error_log /home/bjones/projects/dsusa/var/log/dev.error.log error;

	location / {
		fastcgi_pass djangoappserv;
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
