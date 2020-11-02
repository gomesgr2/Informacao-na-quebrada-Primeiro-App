import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AppService } from './services/app.service';
import {MatCardModule} from '@angular/material/card';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {MatToolbarModule} from '@angular/material/toolbar';
import{MatIconModule} from '@angular/material/icon';
import{MatButtonModule} from '@angular/material/button';
import{MatTabsModule} from '@angular/material/tabs'
import{MatDialogModule, MatDialogRef} from '@angular/material/dialog';
import { FormPostComponent } from './view/form-post/form-post.component'
import {MatFormFieldModule} from '@angular/material/form-field';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import {FlexLayoutModule} from '@angular/flex-layout';
import {CUSTOM_ELEMENTS_SCHEMA} from '@angular/core'
import {MatSelectModule} from '@angular/material/select'
import {MatInputModule} from '@angular/material/input'
import {MatExpansionModule} from '@angular/material/expansion';
import { AboutComponent } from './view/about/about.component';
import { RouterModule } from '@angular/router';


@NgModule({
  declarations: [
    AppComponent,
    FormPostComponent,
    AboutComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule, HttpClientModule,MatCardModule,
    BrowserAnimationsModule,MatToolbarModule,MatIconModule,
    MatButtonModule,MatTabsModule, MatDialogModule,MatFormFieldModule, 
    FormsModule,ReactiveFormsModule, FlexLayoutModule, MatSelectModule,MatInputModule, MatExpansionModule,RouterModule
  ],
    
    providers: [AppService, {provide :MatDialogRef, useValue : {}}, FormPostComponent],
    bootstrap: [AppComponent]
})
export class AppModule{}
