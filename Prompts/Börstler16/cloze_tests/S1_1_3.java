/** 
 * Informs the webmaster of an unexpected problem (Exception “ex”) 
 * with the deployed application (indicated by “aRequest”). 
 */ 
public void logAndEmailSeriousProblem(Throwable ex, HttpServletRequest aRequest) 
{ 
    TroubleTicket troubleTicket = new TroubleTicket(ex, aRequest); 
    
    fLogger.severe("TOP LEVEL CATCHING Throwable."); 
    fLogger.severe(troubleTicket.toString()); 

    log("SERIOUS PROBLEM OCCURRED."); 
    A:_____________________________;

    aRequest.getSession().B:___________________. 
        setAttribute(MOST_RECENT_TROUBLE_TICKET, troubleTicket); 
    troubleTicket.mailToWebmaster(); 
}