/** 
 * Informs the webmaster of an unexpected problem (Exception “ex”) 
 * with the deployed application (indicated by “aRequest”). 
 */ 
public void logAndEmailSeriousProblem(Throwable ex, HttpServletRequest aRequest) 
{ 
    /* Create trouble ticket with context reference. */ 
    TroubleTicket troubleTicket = new TroubleTicket(ex, aRequest); 
    
    /* Log message to file. */ 
    fLogger.severe("TOP LEVEL CATCHING Throwable."); 
    fLogger.severe(troubleTicket.toString()); 
    
    /* Log message to output. */ 
    log("SERIOUS PROBLEM OCCURRED."); 
    A:_____________________________; 
    
    /* Remember most recent ticket and inform webmaster. */ 
    HttpSession session = aRequest.getSession(); 
    B:_____________________ = session.C:_________________; 
    context.setAttribute(MOST_RECENT_TROUBLE_TICKET, troubleTicket); 
    troubleTicket.mailToWebmaster(); 
}