server {
	server_name stage.designserviceusa.com;
 	listen 80 default;
	
	client_max_body_size 10m;

	location ~ /(data|wufu|css|images|js|pic)/ {
		root /var/www/com_designserviceusa_stage/static;
	}

	location ~ /favicon.* {
		root /var/www/com_designserviceusa_stage/static;
	}

	location /files/ {
		alias /var/www/com_designserviceusa_stage/var/application-data/;
	}

        location / {
		include /etc/nginx/fastcgi_params;
                fastcgi_pass unix:/var/www/com_designserviceusa_stage/var/designfirst-fcgi.sock;
                fastcgi_param  HTTPS        on;
                fastcgi_pass_header Authorization;
                fastcgi_intercept_errors off;
        }
}	
