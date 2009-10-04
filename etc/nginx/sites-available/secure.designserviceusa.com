server {
 	listen 443;
	server_name secure.designserviceusa.com;
	
	# ssl params
	keepalive_timeout 70;
	ssl on;
	ssl_certificate /etc/ssl/certs/ssl-cert-com_designserviceusa_secure.pem;
	ssl_certificate_key /etc/ssl/private/ssl-cert-com_designserviceusa_secure.key;
	#ssl_session_cache shared: SSL: 10m;
	#ssl_session_timeout 10m;
	# end ssl params

        location / {
                fastcgi_pass unix:/var/www/com_designserviceusa_beta/var/designfirst.sock;
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
