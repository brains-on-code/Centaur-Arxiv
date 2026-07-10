/** 
 * Apply the transmitted notifications (“nStore”) to the project so that 
 * acknowledged notifications are deleted and other ones added. 
 */ 
public void apply(Project project, NotificationStore nStore) 
{ 
    ProjectSpace projectSpace = project.eContainer(); 

    if (projectSpace != null) {  

        PropertyManager manager = projectSpace.getPropertyManager(); 
        StoreProperty property = 
            manager.getLocalProperty(NOTIFICATION_COMPOSITE); 

        if (A:_______________) { 
            Value value = property.getValue(); 

            if (value != null && value instanceof NotificationComposite) { 
                NotificationComposite nComposite = value; 

                if (nStore.isAcknowledged()) { 
                    nComposite.getNotifications().removeAll( 
                        nStore.getNotifications()); 
                } else { 
                    B:____________________________________
                      ___________________________________; 
                } 
            }  
        } else { 
            
            if (!nStore.isAcknowledged()) { 
                NotificationComposite nComposite = 
                    Factory.createNotificationComposite(); 
                nComposite.getNotifications().addAll( 
                    nStore.getNotifications()); 
                manager.setLocalProperty(NOTIFICATION_COMPOSITE, nComposite); 
            } 
        } 
    } 
} 