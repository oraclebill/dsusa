server {
 	listen 443;
	server_name secure.designserviceusa.com;
	
	# ssl params
	keepalive_timeout 70;
	ssl on;
	ssl_certificate /home/bjones/projects/dsusa/etc/ssl/secure.designserviceusa.com/cert-combined;
	ssl_certificate_key /home/bjones/projects/dsusa/etc/ssl/secure.designserviceusa.com/key;
	#ssl_session_cache shared: SSL: 10m;
	#ssl_session_timeout 10m;
	# end ssl params

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
                fastcgi_param  HTTPS        on;
                fastcgi_pass_header Authorization;
                fastcgi_intercept_errors off;
        }
}	
