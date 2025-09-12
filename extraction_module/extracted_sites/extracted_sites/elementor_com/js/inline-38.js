
wp.apiFetch.use( wp.apiFetch.createRootURLMiddleware( "https://elementor.com/wp-json/" ) );
wp.apiFetch.nonceMiddleware = wp.apiFetch.createNonceMiddleware( "ce0ed85184" );
wp.apiFetch.use( wp.apiFetch.nonceMiddleware );
wp.apiFetch.use( wp.apiFetch.mediaUploadMiddleware );
wp.apiFetch.nonceEndpoint = "https://elementor.com/wp-admin/admin-ajax.php?action=rest-nonce";
