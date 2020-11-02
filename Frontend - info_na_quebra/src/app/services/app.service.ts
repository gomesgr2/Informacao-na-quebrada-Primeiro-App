import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { retry, catchError } from 'rxjs/operators';
import { Podcast } from '../models/podcast';
import {Sites} from '../models/sites'
import {Form} from '../models/form'

@Injectable({
  providedIn: 'root'
})
export class AppService {

  url_podcast = 'http://localhost:5000/Podcast'
  url_sites = 'http://localhost:5000/Sites'
  url_form = 'http://localhost:5000/Sugestoes'

  // injetando o HttpClient
  constructor(private httpClient: HttpClient) { }

  // Headers
  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  }
  PostPodcast(pod: Podcast): Observable<Podcast> {
    return this.httpClient.post<Podcast>(this.url_podcast, JSON.stringify(pod), this.httpOptions)
      .pipe(
        retry(2),
        catchError(this.handleError)
      )
  }
  PostSites(sites: Sites): Observable<Sites> {
    return this.httpClient.post<Sites>(this.url_sites, JSON.stringify(sites), this.httpOptions)
      .pipe(
        retry(2),
        catchError(this.handleError)
      )
  

}
PostForm(form: Form): Observable<Form> {
  return this.httpClient.post<Form>(this.url_form, JSON.stringify(form), this.httpOptions)
    .pipe(
      retry(2),
      catchError(this.handleError)
    ) }

   // Manipulação de erros
  handleError(error: HttpErrorResponse) {
    let errorMessage = '';
    if (error.error instanceof ErrorEvent) {
      // Erro ocorreu no lado do client
      errorMessage = error.error.message;
    } else {
      // Erro ocorreu no lado do servidor
      errorMessage = `Código do erro: ${error.status}, ` + `menssagem: ${error.message}`;
    }
    console.log(errorMessage);
    return throwError(errorMessage);
  };

}

  
