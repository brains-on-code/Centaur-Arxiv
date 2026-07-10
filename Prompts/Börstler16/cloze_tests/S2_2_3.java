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
        NotificationList notifications; 
        
        if (A:________________) { 
            Value value = property.getValue(); 

            if (value != null && value instanceof NotificationComposite) { 
                NotificationComposite nComposite = value; 
                 B:____________ = C:___________________________; 
                
                if (nStore.isAcknowledged()) { 
                    notifications.removeAll(nStore.getNotifications()); 
                } else { 
                    D:______________________________________________
                } 
            }  
        } else { 
            
            if (!nStore.isAcknowledged()) { 
                NotificationComposite nComposite = 
                    Factory.createNotificationComposite(); 
                notifications = nComposite.getNotifications();
                 
                notifications.addAll(nStore.getNotifications()); 
                manager.setLocalProperty(NOTIFICATION_COMPOSITE, nComposite); 
            } 
        } 
    } 
} 
