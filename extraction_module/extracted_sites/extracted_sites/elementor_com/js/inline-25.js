
				addEventListener( 'onSiteCreationStart', function () {
					if ( ! window.braze || ! braze.logCustomEvent ) {
						return;
					}

					braze.logCustomEvent( 'site_creation_start_event' );
				} );
			