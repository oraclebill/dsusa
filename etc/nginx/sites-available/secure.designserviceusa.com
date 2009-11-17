server {
	server_name secure.designserviceusa.com;
 	listen 443 default;
	
	# ssl params
	keepalive_timeout 70;
	ssl on;
	ssl_certificate /etc/ssl/certs/ssl-cert-com_designserviceusa_secure.pem;
	ssl_certificate_key /etc/ssl/private/ssl-cert-com_designserviceusa_secure.key;
	#ssl_session_cache shared: SSL: 10m;
	#ssl_session_timeout 10m;
	# end ssl params

	client_max_body_size 10m;

	location ~ /(data|wufu|css|images|js|pic)/ {
		root /var/www/com_designserviceusa_oneworld/static;
	}

	location ~ /favicon.* {
		root /var/www/com_designserviceusa_oneworld/static;
	}

	location /files/ {
		alias /var/www/com_designserviceusa_oneworld/var/application-data/;
	}

        location / {
		include /etc/nginx/fastcgi_params;
                fastcgi_pass unix:/var/www/com_designserviceusa_oneworld/var/designfirst-fcgi.sock;
                fastcgi_param  HTTPS        on;
                fastcgi_pass_header Authorization;
                fastcgi_intercept_errors off;
        }
}	
