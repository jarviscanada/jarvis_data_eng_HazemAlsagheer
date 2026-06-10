package ca.jrvs.apps.liveCodingPrep;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.Iterator;
import java.util.List;
import java.util.stream.Collectors;

public class ExpenseTracker{
    private List<Expense> list= new ArrayList<>();


    public void addExpense(Expense e){
      if (e==null){
        throw new NullPointerException("Cannot add a null expense");
      }
      this.list.add(e);
    }

    public double totalSpent(){
      return list.stream().mapToDouble(Expense::getAmount).sum();

    }
    public double totalByCategory(String category){
      return list.stream().filter(e->e.getCategory().equals(category)).mapToDouble(Expense::getAmount).sum();
    }


    public String topCategory(){

      return list.stream().max(Comparator.comparingDouble(Expense::getAmount)).map(Expense::getCategory).orElse(null);
    }

  public static void main(String[] args) {
    ExpenseTracker exp= new ExpenseTracker();
    exp.addExpense(new Expense(1000, "Rent","2026-03-01"));
    exp.addExpense(new Expense(20, "Food","2026-03-02"));
    exp.addExpense(new Expense(15, "Food","2026-03-02"));
    exp.addExpense(new Expense(50, "Transport","2026-03-03"));
    exp.addExpense(new Expense(60, "Entertainment","2026-03-03"));

    System.out.println("Total Spent: "+exp.totalSpent());
    System.out.println("Food Total: "+exp.totalByCategory("Food"));
    System.out.println("Transport Total: "+exp.totalByCategory("Transport"));
    System.out.println("Entertainment Total: "+exp.totalByCategory("Entertainment"));
    System.out.println("Rent Total: "+exp.totalByCategory("Rent"));
    System.out.println("Top Category: "+exp.topCategory());

  }

}


